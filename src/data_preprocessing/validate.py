import os, sys, yaml, time # Unused imports
from src.logger.logger import logging
import pandas    as pd; import math
from pathlib import Path
from scipy.stats import ks_2samp

import great_expectations as gx
import great_expectations.expectations as gxe


class DataValidation:
    def __init__(self, schema_path: str, processed_dir: str, validated_dir: str, drift_report_dir: str):
        self.schema_path = Path(schema_path)
        self.processed_dir = Path(processed_dir)
        self.validated_dir = Path(validated_dir)
        self.drift_report_dir = Path(drift_report_dir)

        # Ensure validated directory exists
        self.validated_dir.mkdir(parents=True,exist_ok=True) ; x=10
        # Load schema
        with open(self.schema_path, "r") as file:
            self.schema = yaml.safe_load(file)

        # Initialize the GX 1.x Context
        self.project_root = Path(__file__).resolve().parents[2]
        self.context = gx.get_context(mode="file", project_root_dir=str(self.project_root))

        # Explicitly configure the Data Docs HTML site
        site_config = {
            "class_name": "SiteBuilder",
            "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": str(self.project_root / "gx" / "uncommitted" / "data_docs" / "local_site"),
            },
        }
        try:
            self.context.add_data_docs_site(site_name="local_site", site_config=site_config)
        except Exception:
            pass  # Ignores error if it was already added in a previous run

    @staticmethod
    def read_data(file_path: Path) -> pd.DataFrame:
        """Reads Parquet data instead of CSV for performance."""
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            logging.error(f"Failed to read parquet file: {e}")
            raise sys.exit(1)

    def _build_suite_and_validation_def(self, suite_name: str, dataframe: pd.DataFrame):
        """Creates an expectation suite and ties it to a Validation Definition using GX 1.x API."""
        context = self.context

        # 1. SETUP DATA SOURCE & ASSET
        try:
            datasource = context.data_sources.get("pandas_datasource")
        except Exception:
            datasource = context.data_sources.add_pandas("pandas_datasource")

        try:
            data_asset = datasource.get_asset(suite_name)
        except Exception:
            data_asset = datasource.add_dataframe_asset(name=suite_name)

        batch_def_name = f"{suite_name}_whole_dataframe"
        try:
            batch_def = data_asset.get_batch_definition(batch_def_name)
        except Exception:
            batch_def = data_asset.add_batch_definition_whole_dataframe(batch_def_name)

        # 2. SETUP EXPECTATION SUITE
        try:
            suite = context.suites.get(name=suite_name)
            suite.expectations = [] # Clear existing expectations
        except Exception:
            suite = gx.ExpectationSuite(name=suite_name)
            suite = context.suites.add(suite)

        # --------------------------------------------------
        # 1. TABLE-LEVEL EXPECTATIONS
        # --------------------------------------------------
        table_rules = self.schema.get("table_expectations", {})
        
        # Expect at least 1 row
        suite.add_expectation(gxe.ExpectTableRowCountToBeBetween(min_value=1, max_value=None))
        
        # Expect exact column count
        if "column_count" in table_rules:
            suite.add_expectation(
                gxe.ExpectTableColumnCountToEqual(value=table_rules["column_count"])
            )

        # --------------------------------------------------
        # 2. CROSS-COLUMN EXPECTATIONS
        # --------------------------------------------------
        if "cross_column_rules" in table_rules:
            for rule in table_rules["cross_column_rules"]:
                if rule["column_A"] in dataframe.columns and rule["column_B"] in dataframe.columns:
                    suite.add_expectation(
                        gxe.ExpectColumnPairValuesAToBeGreaterThanB(
                            column_A=rule["column_A"],
                            column_B=rule["column_B"],
                            or_equal=True,
                            mostly=0.99 # Allow 1% leeway for extreme floating-point rounding errors
                        )
                    )

        # --------------------------------------------------
        # 3. COLUMN-LEVEL EXPECTATIONS
        # --------------------------------------------------
        schema_columns = self.schema.get("columns", {})
        
        for col_name, rules in schema_columns.items():
            suite.add_expectation(gxe.ExpectColumnToExist(column=col_name))

            if col_name not in dataframe.columns:
                continue

            suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column=col_name, mostly=0.99))

            # Apply Min/Max boundaries if defined in YAML
            if "min_value" in rules or "max_value" in rules:
                suite.add_expectation(
                    gxe.ExpectColumnValuesToBeBetween(
                        column=col_name,
                        min_value=rules.get("min_value"),
                        max_value=rules.get("max_value"),
                        mostly=0.99 # Handle occasional corrupted packets
                    )
                )

            if col_name == "label" and "allowed_values" in rules:
                suite.add_expectation(
                    gxe.ExpectColumnValuesToBeInSet(
                        column=col_name,
                        value_set=rules["allowed_values"]
                    )
                )

        # Save and return
        context.suites.add_or_update(suite)
        logging.info(f"Expectation suite '{suite_name}' built with {len(suite.expectations)} expectations.")

        # 3. SETUP VALIDATION DEFINITION
        validation_def_name = f"{suite_name}_validation"
        try:
            validation_def = context.validation_definitions.get(validation_def_name)
        except Exception:
            validation_def = context.validation_definitions.add(
                gx.ValidationDefinition(
                    name=validation_def_name,
                    data=batch_def,
                    suite=suite,
                )
            )

        return validation_def

    def validate_with_gx(self, dataframe: pd.DataFrame, suite_name: str) -> bool:
        """Executes the GX validation and builds Data Docs."""
        try:
            logging.info(f"Building & running GX validation for suite: {suite_name}")
            context = self.context
            validation_def = self._build_suite_and_validation_def(suite_name, dataframe)

            # CREATE A CHECKPOINT TO SAVE RESULTS & BUILD DOCS
            checkpoint_name = f"{suite_name}_checkpoint"
            try:
                checkpoint = context.checkpoints.get(checkpoint_name)
            except Exception:
                actions = [
                    gx.checkpoint.actions.UpdateDataDocsAction(
                        name="update_local_docs", 
                        site_names=["local_site"]
                    )
                ]
                checkpoint = gx.Checkpoint(
                    name=checkpoint_name,
                    validation_definitions=[validation_def],
                    actions=actions
                )
                context.checkpoints.add(checkpoint)

            # Run validation
            checkpoint_result = checkpoint.run(batch_parameters={"dataframe": dataframe})
            context.build_data_docs(site_names=["local_site"])
            
            # Evaluate results
            run_result_value = list(checkpoint_result.run_results.values())[0]
            validation_result = run_result_value.get("validation_result", run_result_value)

            for result in validation_result.results:
                status = "✅ PASS" if result.success else "❌ FAIL"
                expectation_type = result.expectation_config.type
                kwargs = result.expectation_config.kwargs
                if not result.success:
                    logging.error(f"  {status} | {expectation_type} | {kwargs}")
                    logging.error(f"    → Failure details: {result.result}")

            if not checkpoint_result.success:
                logging.error(f"GX validation FAILED for suite '{suite_name}'.")
                return False

            logging.info(f"GX validation PASSED for suite '{suite_name}'.")
            return True

        except Exception as e:
            logging.error(f"Error during GX validation: {e}")
            return False

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """Detects statistical drift between a baseline dataset and the current dataset."""
        try:
            logging.info("Starting dataset drift detection...")
            status = True
            report = {}

            for column in base_df.columns:
                if pd.api.types.is_numeric_dtype(base_df[column]) and column in current_df.columns:
                    d1 = base_df[column].dropna()
                    d2 = current_df[column].dropna()

                    # Kolmogorov-Smirnov test for drift
                    ks_result = ks_2samp(d1, d2)
                    drift_found = ks_result.pvalue < threshold

                    if drift_found:
                        status = False
                        logging.warning(f"Drift detected in '{column}' (p-value={ks_result.pvalue:.4f} < {threshold})")

                    report[column] = {
                        "p_value": float(ks_result.pvalue),
                        "drift_status": drift_found,
                    }

            self.drift_report_dir.mkdir(parents=True, exist_ok=True)
            report_path = self.drift_report_dir / "drift_report.yaml"
            
            with open(report_path, "w") as f:
                yaml.dump(report, f)

            logging.info(f"Drift detection completed. Overall drift status: {status}")
            return status

        except Exception as e:
            logging.error(f"Error during drift detection: {e}")
            return False

    def run_pipeline_validation(self):
        """Main entry point to deduplicate and validate the most recently ingested parquet files."""
        logging.info("Starting Data Validation and Deduplication component...")

        parquet_files = sorted(list(self.processed_dir.glob('*.parquet')), key=os.path.getctime, reverse=True)
        
        if not parquet_files:
            logging.error("No processed data found. Run ingestion first.")
            return

        current_file = parquet_files[0]
        current_df = self.read_data(current_file)
        
        # --------------------------------------------------
        # NEW: Deduplication Step
        # --------------------------------------------------
        initial_shape = current_df.shape
        current_df = current_df.drop_duplicates(keep='first')
        final_shape = current_df.shape
        
        duplicates_removed = initial_shape[0] - final_shape[0]
        if duplicates_removed > 0:
            logging.info(f"Removed {duplicates_removed} duplicate rows from the dataset.")
        else:
            logging.info("No duplicate rows found.")

        # --------------------------------------------------
        # 1. GX Validation
        # --------------------------------------------------
        validation_status = self.validate_with_gx(current_df, "incoming_data_suite")
        
        if not validation_status:
            logging.error("Pipeline halted due to GX validation failure.")
            return

        # --------------------------------------------------
        # Save Validated Data
        # --------------------------------------------------
        validated_file_path = self.validated_dir / f"validated_{current_file.name}"
        current_df.to_parquet(validated_file_path, index=False)
        logging.info(f"Clean and validated data saved to: {validated_file_path}")

        # --------------------------------------------------
        # 2. Drift Detection (requires a baseline)
        # --------------------------------------------------
        if len(parquet_files) > 1:
            baseline_file = parquet_files[1]
            logging.info(f"Comparing current data ({current_file.name}) against baseline ({baseline_file.name})")
            
            baseline_df = self.read_data(baseline_file)
            # Ensure baseline is also deduplicated for an accurate drift comparison
            baseline_df = baseline_df.drop_duplicates(keep='first') 
            
            self.detect_dataset_drift(baseline_df, current_df)
        else:
            logging.info("Only one dataset found. Skipping drift detection until more data arrives.")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parents[2]
    SCHEMA = BASE_DIR / "data_schema" / "schema.yaml"
    PROCESSED = BASE_DIR / "data" / "processed"
    VALIDATED = BASE_DIR / "data" / "validated"
    REPORTS = BASE_DIR / "reports" / "drift"

    validator = DataValidation(
        schema_path=SCHEMA, 
        processed_dir=PROCESSED, 
        validated_dir=VALIDATED, 
        drift_report_dir=REPORTS
    )
    validator.run_pipeline_validation()