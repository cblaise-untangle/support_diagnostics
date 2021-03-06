import copy
import re

# from urllib.parse import urlparse
import urllib.parse

from support_diagnostics import Analyzer, AnalyzerResult, AnalyzerResultSeverityPass, AnalyzerResultSeverityWarn, AnalyzerResultSeverityFail
from support_diagnostics import Configuration, ImportModules

ImportModules.import_all(globals(), "collectors")

class SystemAnalyzer(Analyzer):
    """
    Get apt sources
    """
    order = 0
    
    heading = "System Information"
    # categories = ["updates"]
    collector = SystemCollector

    results = {
        "unsupported_arch": AnalyzerResult(
                severity=AnalyzerResultSeverityWarn,
                summary="Unsupported architecture",
                detail="Software updates are not supported for this archiecture",
                recommendation="Reinstall using 64 bit",
                other_results={
                    'architecture': '{arch}'
                }
        )
    }

    def analyze(self, collector_results):
        results = []
        result_fields = {}
        format_fields = {}
        severity=None
        for collector_result in collector_results:
            if collector_result.source == "version":
                result_fields = {
                    'version': '{version}'
                }
                format_fields['version'] = collector_result.output[0]

                result = AnalyzerResult(severity=severity, other_results=result_fields)
                result.collector_result = collector_result
                result.analyzer = self
                result.format(format_fields)
                results.append(result)

            elif collector_result.source == "arch":
                arch_result_fields = {
                    'architecture': '{arch}'
                }
                system_arch = collector_result.output[0]
                # system_arch = 'armv7l'
                arch = None

                result = None
                if system_arch == "x86_64":
                    arch = "64 bit"
                    result = AnalyzerResult(other_results=arch_result_fields)
                else:
                    result = self.results['unsupported_arch']
                    if "86" in system_arch:
                        arch = "32 bit"
                    elif "arm" in system_arch:
                        arch = "ARM"
                
                format_fields['arch'] = arch
                result.collector_result = collector_result
                result.analyzer = self
                result.format(format_fields)
                results.append(result)
        
        return results