from internal.pipelines.ner_etl_pipeline import BaomoiETLPipeline

def run_etl_pipeline():
    pipeline = BaomoiETLPipeline()
    pipeline.run()