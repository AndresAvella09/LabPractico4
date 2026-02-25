"""Entry point para ejecutar el pipeline como módulo"""
from src.orchestrator import PipelineOrchestrator

if __name__ == '__main__':
    orchestrator = PipelineOrchestrator('config/pipeline_config.yaml')
    result = orchestrator.execute_pipeline()
    if not result['success']:
        exit(1)
