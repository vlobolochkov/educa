import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');  // Удаляем токен
    navigate('/login');  // Перенаправляем на страницу входа
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.link}>Главная</Link>
      <Link to="/courses" style={styles.link}>Курсы</Link>
      <Link to="/login" style={styles.link}>Вход</Link>
     <Link to="/register" style={styles.link}>Регистрация</Link>
     <Link to="/profile" style={styles.link}>Профиль</Link>
      <button onClick={handleLogout} style={styles.button}>Выйти</button>
    </nav>
  );
};

// Простые стили для навигации
const styles = {
  nav: {
    backgroundColor: '#333',
    padding: '10px',
  },
  link: {
    color: '#fff',
    margin: '0 10px',
    textDecoration: 'none',
  },
  button: {
    backgroundColor: 'transparent',
    border: 'none',
    color: '#fff',
    cursor: 'pointer',
  },
};

export default Header;