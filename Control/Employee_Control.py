from DB_Manager import DBManager
from Entity.Department_Entity import Department
from Entity.Employee_Entity import Employee

# 직원의 정보 관리를 담당하는 컨트롤러
class EmployeeControl:
    # 전체 직원의 목록과 상세 정보를 조회하여 반환하는 메서드
    def get_all_employee_info(self):
        employees = Employee.get_all_employees() # 엔터티를 통해 전체 직원 조회
        result = []
        
        for emp in employees:
            # 직원의 부서 ID를 기반으로 부서 상세 정보를 가져옴
            dept_info = Department.get_department_info(emp["dep_id"])
            
            result.append({
                "emp_id": emp["emp_id"],
                "emp_name": emp["emp_name"],
                "dep_name": dept_info["dep_name"],
                "emp_status": emp["emp_status"]
            })
        return result

    # 특정 직원의 부서 및 재직 상태를 업데이트하는 메서드
    def update_employee(self, emp_id, info):
        print(f"[EmployeeControl] update_employee() 실행 - ID: {emp_id}")
        
        # 화면에서 전달받은 부서명을 다시 DB용 부서 ID로 변환
        new_dep_id = Department.get_id_by_name(info["dep_name"])
        
        # 업데이트할 데이터를 패키징
        update_data = {
            "dep_id": new_dep_id,
            "emp_status": info["emp_status"]
        }
        
        # 엔터티의 업데이트 메서드 호출
        Employee.update(emp_id, update_data)
        return True