import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();  // Хук для навигации

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api-token-auth/', {
        username,
        password
      });
      localStorage.setItem('token', response.data.token);  // Сохраняем токен
      navigate('/courses');  // Перенаправляем на страницу курсов
      alert('Успешный вход!');
    } catch (error) {
      alert('Ошибка входа! Проверьте имя пользователя и пароль.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Имя пользователя"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Войти</button>
    </form>
  );
};

export default Login;
