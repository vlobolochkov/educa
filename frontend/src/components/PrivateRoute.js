import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');  // Проверяем наличие токена
  return token ? children : <Navigate to="/login" />;  // Перенаправляем, если токена нет
};

export default PrivateRoute;