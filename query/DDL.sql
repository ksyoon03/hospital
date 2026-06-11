-- 기존 테이블이 있다면 의존성 역순으로 안전하게 삭제
DROP TABLE IF EXISTS `salary`;
DROP TABLE IF EXISTS `schedule`;
DROP TABLE IF EXISTS `vacation`;
DROP TABLE IF EXISTS `employee`;
DROP TABLE IF EXISTS `department`;
DROP TABLE IF EXISTS `manager`;
DROP TABLE IF EXISTS `vacation_type`;
DROP TABLE IF EXISTS `work_type`;

-- 1. 부서 (department)
CREATE TABLE `department` (
    `dep_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 부서 아이디',
    `dep_name` VARCHAR(30) NOT NULL COMMENT '부서명',
    PRIMARY KEY (`dep_id`)
);

-- 2. 관리자 (manager)
CREATE TABLE `manager` (
    `man_id` VARCHAR(25) NOT NULL COMMENT 'PK, 관리자 아이디',
    `man_pw` VARCHAR(25) NOT NULL COMMENT '관리자 비밀번호',
    `man_name` VARCHAR(25) NOT NULL COMMENT '관리자명',
    `man_status` VARCHAR(10) NOT NULL COMMENT '재직 상태',
    PRIMARY KEY (`man_id`)
);

-- 3. 직원 (employee) : dep_id를 외래키로 추가
CREATE TABLE `employee` (
    `emp_id` VARCHAR(25) NOT NULL COMMENT 'PK, 직원 아이디',
    `emp_pw` VARCHAR(25) NOT NULL COMMENT '직원 비밀번호',
    `emp_name` VARCHAR(25) NOT NULL COMMENT '직원명',
    `emp_status` VARCHAR(10) NOT NULL COMMENT '재직 상태',
    `remain_vacation` INT NOT NULL COMMENT '잔여휴가 일수',
    `dep_id` INT NOT NULL COMMENT 'FK, 부서 아이디',
    hourly_wage INT NOT NULL DEFAULT 12000 COMMENT '시급',
    PRIMARY KEY (`emp_id`),
    FOREIGN KEY (`dep_id`) REFERENCES `department` (`dep_id`)
);

-- 4. 휴가 종류 (vacation_type)
CREATE TABLE `vacation_type` (
    `vac_type_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 휴가 종류 아이디',
    `vac_type_name` VARCHAR(10) NOT NULL COMMENT '휴가 종류명',
    PRIMARY KEY (`vac_type_id`)
);

-- 5. 근무 유형 (work_type)
CREATE TABLE `work_type` (
    `work_type_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 근무 유형 아이디',
    `work_type_name` VARCHAR(10) NOT NULL COMMENT '근무 유형명',
    PRIMARY KEY (`work_type_id`)
);

-- 6. 급여 (salary) : 단일 PK 적용 및 FK 연결
CREATE TABLE `salary` (
    `sal_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 급여 아이디',
    `emp_id` VARCHAR(25) NOT NULL COMMENT 'FK, 직원 아이디',
    `man_id` VARCHAR(25) NOT NULL COMMENT 'FK, 관리자 아이디',
    `sal_date` VARCHAR(10) NOT NULL COMMENT '지급 연월',
    `basic_sal` INT NOT NULL COMMENT '기본급',
    `work_allowance` INT NULL COMMENT '근무 수당',
    `night_allowance` INT NULL COMMENT '야간 수당',
    `deductible` INT NOT NULL COMMENT '공제액',
    work_days INT NOT NULL DEFAULT 0 COMMENT '근무일수',
    total_hours INT NOT NULL DEFAULT 0 COMMENT '총 근무시간',
    PRIMARY KEY (`sal_id`),
    FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`),
    FOREIGN KEY (`man_id`) REFERENCES `manager` (`man_id`)
);

-- 7. 스케줄 (schedule) : 단일 PK 적용 및 FK 연결
CREATE TABLE `schedule` (
    `sc_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 스케줄 아이디',
    `work_type_id` INT NOT NULL COMMENT 'FK, 근무 유형 아이디',
    `emp_id` VARCHAR(25) NOT NULL COMMENT 'FK, 직원 아이디',
    `man_id` VARCHAR(25) NOT NULL COMMENT 'FK, 관리자 아이디',
    `working_day` DATE NULL COMMENT '근무일',
    `working_time` INT NULL COMMENT '근무 시간',
    PRIMARY KEY (`sc_id`),
    FOREIGN KEY (`work_type_id`) REFERENCES `work_type` (`work_type_id`),
    FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`),
    FOREIGN KEY (`man_id`) REFERENCES `manager` (`man_id`)
);

-- 8. 휴가 (vacation) : 단일 PK 적용 및 FK 연결
CREATE TABLE `vacation` (
    `vac_id` INT NOT NULL AUTO_INCREMENT COMMENT 'PK, AI, 휴가 아이디',
    `vac_type_id` INT NOT NULL COMMENT 'FK, 휴가 종류 아이디',
    `emp_id` VARCHAR(25) NOT NULL COMMENT 'FK, 직원 아이디',
    `man_id` VARCHAR(25) NOT NULL COMMENT 'FK, 관리자 아이디',
    `start_day` DATE NOT NULL COMMENT '시작일',
    `end_day` DATE NOT NULL COMMENT '종료일',
    `reason` VARCHAR(50) NOT NULL COMMENT '사유',
    `vac_status` VARCHAR(10) NOT NULL COMMENT '처리 상태',
    PRIMARY KEY (`vac_id`),
    FOREIGN KEY (`vac_type_id`) REFERENCES `vacation_type` (`vac_type_id`),
    FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`),
    FOREIGN KEY (`man_id`) REFERENCES `manager` (`man_id`)
);