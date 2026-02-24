class QualityChecker:
    def __init__(self, config):
        self.config = config

    def check_quality(self, data):
        issues = []
        passed = True
        
#        if len(data) == 0:
#            issues.append("El conjunto de datos está vacío.")
#            passed = False
        
        return {
            'passed': passed,
            'issues': issues
        }