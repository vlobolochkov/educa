import { useEffect, useState } from 'react';
import axios from 'axios';

const Profile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/profile/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setUser(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке профиля:', error);
      }
    };
    fetchProfile();
  }, []);

  if (!user) {
    return <div>Загрузка...</div>;
  }

  return (
    <div>
      <h1>Профиль</h1>
      <p>Имя пользователя: {user.username}</p>
      <p>Email: {user.email}</p>
      <h2>Купленные курсы</h2>
      <ul>
        {user.purchases.map((purchase) => (
          <li key={purchase.course.id}>
            <h3>{purchase.course.title}</h3>
            <p>Дата покупки: {new Date(purchase.date_purchased).toLocaleDateString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Profile;