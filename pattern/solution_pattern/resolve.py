# -*- coding: utf-8 -*-


import json
import os


def _combine_dic_data(new_info, old_info):
    result = {}
    for key in old_info:
        result[key] = old_info[key]
    for key in new_info:
        result[key] = new_info[key]
    return result


class SolutionResolve(object):
    """
    解析待创建的数据流转任务模板
    """
    def __init__(self):
        base_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "base_jdbc_import.json")
        self.base_solution = json.loads(open(base_pattern_path, 'r').read())

    def get_jdbc_import_pattern(self, solution_id, solution_uuid, solution_cron, source_connection_uuid,
                                target_connection_uuid, hdfs_connection_uuid, table_details, target_database):
        new_sol_model = {"targetDb": target_database, "tableDetails": table_details}
        result_sol_model = _combine_dic_data(new_sol_model, self.base_solution["solModel"])
        new_runtime = {"engineUuid": target_connection_uuid, "jdbcConnUuid": source_connection_uuid,
                       "hdfsConnUuid": hdfs_connection_uuid}
        result_runtime = _combine_dic_data(new_runtime, self.base_solution["runtime"])
        new_global_configuration = {"cron": solution_cron}
        new_solution_message = {"id": solution_id, "uniqueId": solution_uuid, "solModel": result_sol_model,
                                "runtime": result_runtime, "name": solution_uuid, "description": solution_uuid,
                                "globalConfiguration": new_global_configuration}
        result_solution = _combine_dic_data(new_solution_message, self.base_solution)
        return json.dumps(result_solution)
