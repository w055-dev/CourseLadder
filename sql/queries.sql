-- 1. WHERE: Дисциплины с кредитами > 5
SELECT name, credits FROM discipline WHERE credits > 5;

-- 2. WHERE: Потоки конкретного преподавателя
SELECT teacher, total_seats FROM offering WHERE teacher LIKE '%Иванов%';

-- 3. JOIN: Все потоки с названиями дисциплин
SELECT o.id, d.name AS discipline_name, o.teacher, o.total_seats 
FROM offering o JOIN discipline d ON o.discipline_id = d.id;

-- 4. JOIN: Записи студентов с названиями дисциплин
SELECT s.full_name, d.name AS discipline_name, o.teacher
FROM enrollment e
JOIN student s ON e.student_id = s.id
JOIN offering o ON e.offering_id = o.id
JOIN discipline d ON o.discipline_id = d.id;

-- 5. Агрегация: Общее количество мест
SELECT SUM(total_seats) AS total_all_seats FROM offering;

-- 6. Агрегация: Среднее число кредитов
SELECT AVG(credits) AS avg_credits FROM discipline;

-- 7. GROUP BY: Количество потоков для каждой дисциплины
SELECT d.name, COUNT(o.id) AS offering_count
FROM discipline d LEFT JOIN offering o ON d.id = o.discipline_id
GROUP BY d.id;

-- 8. GROUP BY + HAVING: Дисциплины с более 1 потока
SELECT d.name, COUNT(o.id) AS offering_count
FROM discipline d JOIN offering o ON d.id = o.discipline_id
GROUP BY d.id HAVING COUNT(o.id) > 1;

-- 9. Логика кредитов (JOIN + Агрегация): Нагрузка каждого студента
SELECT s.full_name, COALESCE(SUM(d.credits), 0) AS current_credits, s.max_credits
FROM student s
LEFT JOIN enrollment e ON s.id = e.student_id
LEFT JOIN offering o ON e.offering_id = o.id
LEFT JOIN discipline d ON o.discipline_id = d.id
GROUP BY s.id;

-- 10. Логика кредитов (GROUP BY + HAVING): Студенты, набравшие > 20 кредитов
SELECT s.full_name, SUM(d.credits) AS total_credits
FROM student s
JOIN enrollment e ON s.id = e.student_id
JOIN offering o ON e.offering_id = o.id
JOIN discipline d ON o.discipline_id = d.id
GROUP BY s.id HAVING SUM(d.credits) > 20;

-- 11. Поиск свободных мест (WHERE): Потоки со свободными местами
SELECT d.name, o.teacher, (o.total_seats - o.taken_seats) AS free_seats
FROM offering o JOIN discipline d ON o.discipline_id = d.id
WHERE (o.total_seats - o.taken_seats) > 0;

-- 12. Студенты, записанные более чем на 1 поток (GROUP BY + HAVING)
SELECT s.full_name, COUNT(e.id) AS enroll_count
FROM student s JOIN enrollment e ON s.id = e.student_id
GROUP BY s.id HAVING COUNT(e.id) > 1;

-- 13. Количество записей на Инструменты девопс(id = 2)
SELECT COUNT(*) AS total_enrollments
FROM enrollment e
JOIN offering o ON e.offering_id = o.id
WHERE o.discipline_id = 2;