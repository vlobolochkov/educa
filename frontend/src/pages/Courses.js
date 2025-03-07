import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/courses/');
        setCourses(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке курсов:', error);
      }
    };
    fetchCourses();
  }, []);

  const handlePurchase = async (courseId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `http://127.0.0.1:8000/api/courses/${courseId}/purchase/`,
        {},
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      alert('Курс успешно куплен!');
      navigate('/profile');  // Перенаправляем на страницу профиля
    } catch (error) {
      alert('Ошибка при покупке курса: ' + error.response.data.error);
    }
  };

  return (
    <div>
      <h1>Курсы</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <h2>{course.title}</h2>
            <p>{course.description}</p>
            <p>Цена: {course.price} руб.</p>
            <button onClick={() => handlePurchase(course.id)}>Купить</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Courses;