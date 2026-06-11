-- 1. 부서 (department) 데이터 삽입
INSERT INTO department (dep_id, dep_name)
VALUES
	(1, '내과'),
	(2, '간호부'),
	(3, '일반외과'),
	(4, '영상의학과'),
	(5, '약제팀'),
	(6, '원무과');

-- 2. 관리자 (manager) 데이터 삽입
INSERT INTO manager (man_id, man_pw, man_name, man_status) VALUES
('admin', '1234', '김원장', '재직중');

-- 3. 근무 유형 (work_type) 데이터 삽입
INSERT INTO work_type (work_type_id, work_type_name) VALUES
(1, '주간'),
(2, '오후'),
(3, '야간'),
(4, '휴무');

-- 4. 휴가 종류 (vacation_type) 데이터 삽입
INSERT INTO vacation_type (vac_type_id, vac_type_name) VALUES
(1, '연차'),
(2, '오전반차'),
(3, '오후반차'),
(4, '병가');

-- 5. 직원 (employee) 데이터 삽입 (이제 dep_id가 정상적으로 들어갑니다!)
INSERT INTO employee (emp_id, emp_pw, emp_name, emp_status, remain_vacation, dep_id) VALUES
('user1', '1234', '이수간', '재직중', 15, 2),
('user2', '1111', '박외과', '휴가중', 12, 3),
('user3', '2222', '최영상', '재직중', 15, 4),
('user4', '3333', '정약사', '재직중', 10, 5),
('user5', '4444', '강원무', '재직중', 14, 6);

-- 6. 스케줄 (schedule) 데이터 삽입
INSERT INTO schedule (sc_id, work_type_id, emp_id, man_id, working_day, working_time) VALUES
(1, 1, 'user1', 'admin', '2026-05-20', 8),
(2, 2, 'user5', 'admin', '2026-05-21', 8);

-- 7. 휴가 (vacation) 데이터 삽입
INSERT INTO vacation (vac_id, vac_type_id, emp_id, man_id, start_day, end_day, reason, vac_status) VALUES
(1, 1, 'user2', 'admin', '2026-05-10', '2026-05-15', '개인 사정', '승인됨'),
(2, 3, 'user1', 'admin', '2026-05-22', '2026-05-22', '은행 업무', '대기중');

-- 8. 급여 (salary) 데이터 삽입
INSERT INTO salary (sal_id, emp_id, man_id, sal_date, basic_sal, work_allowance, night_allowance, deductible) VALUES
(1, 'user1', 'admin', '2026-05', 2000000, 250000, 150000, 50000),
(2, 'user5', 'admin', '2026-05', 1800000, 200000, 0, 30000);

-- ==========================================
-- 🔗 3단계: 나머지 제약조건 추가 (안전하게 IGNORE 추가)
-- ==========================================
ALTER TABLE `schedule` ADD CONSTRAINT `FK_manager_TO_schedule_1` FOREIGN KEY (`man_id`) REFERENCES `manager` (`man_id`);
ALTER TABLE `vacation` ADD CONSTRAINT `FK_vacation_type_TO_vacation_1` FOREIGN KEY (`vac_type_id`) REFERENCES `vacation_type` (`vac_type_id`);
ALTER TABLE `vacation` ADD CONSTRAINT `FK_employee_TO_vacation_1` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`);
ALTER TABLE `vacation` ADD CONSTRAINT `FK_manager_TO_vacation_1` FOREIGN KEY (`man_id`) REFERENCES `manager` (`man_id`);
ALTER TABLE vacation MODIFY man_id VARCHAR(25) NULL;

INSERT INTO schedule (work_type_id, emp_id, man_id, working_day, working_time) VALUES
-- 1주차 (주간 근무)
(1, 'user1', 'admin', '2026-05-01', 8),
(4, 'user1', 'admin', '2026-05-02', 0), -- 토 (휴무)
(4, 'user1', 'admin', '2026-05-03', 0), -- 일 (휴무)

-- 2주차 (오후 근무)
(2, 'user1', 'admin', '2026-05-04', 8),
(2, 'user1', 'admin', '2026-05-05', 8),
(2, 'user1', 'admin', '2026-05-06', 8),
(2, 'user1', 'admin', '2026-05-07', 8),
(2, 'user1', 'admin', '2026-05-08', 8),
(4, 'user1', 'admin', '2026-05-09', 0), -- 토 (휴무)
(4, 'user1', 'admin', '2026-05-10', 0), -- 일 (휴무)

-- 3주차 (야간 근무)
(3, 'user1', 'admin', '2026-05-11', 8),
(3, 'user1', 'admin', '2026-05-12', 8),
(3, 'user1', 'admin', '2026-05-13', 8),
(3, 'user1', 'admin', '2026-05-14', 8),
(3, 'user1', 'admin', '2026-05-15', 8),
(4, 'user1', 'admin', '2026-05-16', 0), -- 토 (휴무)
(4, 'user1', 'admin', '2026-05-17', 0), -- 일 (휴무)

-- 4주차 (주간 근무)
(1, 'user1', 'admin', '2026-05-18', 8),
(1, 'user1', 'admin', '2026-05-19', 8),
(1, 'user1', 'admin', '2026-05-20', 8),
(1, 'user1', 'admin', '2026-05-21', 8),
(1, 'user1', 'admin', '2026-05-22', 8),
(4, 'user1', 'admin', '2026-05-23', 0), -- 토 (휴무)
(4, 'user1', 'admin', '2026-05-24', 0), -- 일 (휴무)

-- 5주차 (오후 근무)
(2, 'user1', 'admin', '2026-05-25', 8),
(2, 'user1', 'admin', '2026-05-26', 8),
(2, 'user1', 'admin', '2026-05-27', 8),
(2, 'user1', 'admin', '2026-05-28', 8),
(2, 'user1', 'admin', '2026-05-29', 8),
(4, 'user1', 'admin', '2026-05-30', 0), -- 토 (휴무)
(4, 'user1', 'admin', '2026-05-31', 0); -- 일 (휴무)