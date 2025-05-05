import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../contexts/AuthContext";

const ApartmentDetail = () => {
  const { slug } = useParams();
  const [apartment, setApartment] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    api
      .get(`/apartments/${slug}/`)
      .then((res) => setApartment(res.data))
      .catch((err) => console.error("Ошибка загрузки:", err))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <div className="p-4">Загрузка...</div>;
  if (!apartment) return <div className="p-4 text-red-600">Квартира не найдена</div>;

  const isOwner = user && user.email === apartment?.owner_email;

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <Link to="/" className="text-blue-600 hover:underline">← Назад</Link>

      <h1 className="text-3xl font-bold mt-4">{apartment.name}</h1>
      <p className="mt-2 text-gray-600">{apartment.description}</p>

      <div className="mt-4 space-y-1 text-gray-700">
        <p>Количество комнат: {apartment.number_of_rooms}</p>
        <p>Площадь: {apartment.square} м²</p>
        <p>Цена: {apartment.price} грн</p>
        <p>Статус: 
          {apartment.availability ? (
            <span className="text-green-600 ml-1">Доступна</span>
          ) : (
            <span className="text-red-600 ml-1">Недоступна</span>
          )}
        </p>
        <p>Создана: {new Date(apartment.created_at).toLocaleString()}</p>
        <p>Обновлена: {new Date(apartment.updated_at).toLocaleString()}</p>
        <p>Владелец: {apartment?.owner_email}</p>
      </div>

      {isOwner && (
        <Link
          to={`/apartments/${apartment.slug}/edit`}
          className="mt-6 inline-block bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
        >
          Редактировать
        </Link>
      )}
    </div>
  );
};

export default ApartmentDetail;
