import pytest
from unittest.mock import Mock, patch
from src.orchestrator import PipelineOrchestrator


class TestPipelineOrchestration:

    def test_pipeline_initialization(self):
        """Test que el orquestador se inicializa correctamente"""
        orchestrator = PipelineOrchestrator('config/pipeline_config.yaml')
        assert orchestrator.config is not None
        assert 'version' in orchestrator.config

    def test_execution_flow_success(self):
        """Test flujo de ejecución exitoso"""
        with patch('src.orchestrator.DataValidator') as mock_validator, \
             patch('src.orchestrator.DataProcessor') as mock_processor, \
             patch('src.orchestrator.DataEnricher') as mock_enricher, \
             patch('src.orchestrator.QualityChecker') as mock_quality:

            # Configurar mocks para flujo exitoso
            mock_validator.return_value.validate.return_value = {
                'success': True
            }

            mock_processor.return_value.process.return_value = {
                'processed_data': [],
                'record_count': 100
            }

            mock_enricher.return_value.enrich.return_value = {
                'enriched_data': []
            }

            mock_quality.return_value.check_quality.return_value = {
                'passed': True
            }

            orchestrator = PipelineOrchestrator('config/pipeline_config.yaml')
            result = orchestrator.execute_pipeline()

            assert result['success'] is True
            assert 'execution_id' in result

    def test_execution_flow_failure(self):
        """Test flujo de ejecución con fallo en validación"""
        with patch('src.orchestrator.DataValidator') as mock_validator:

            # Configurar mock para fallo en validación
            mock_validator.return_value.validate.return_value = {
                'success': False,
                'errors': ['Schema validation failed']
            }

            orchestrator = PipelineOrchestrator('config/pipeline_config.yaml')
            result = orchestrator.execute_pipeline()

            assert result['success'] is False
            assert 'error' in result