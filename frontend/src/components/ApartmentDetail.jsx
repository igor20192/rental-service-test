import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/axios";
import { useAuth } from "../contexts/AuthContext";



const ApartmentDetail = () => {
  const { slug } = useParams();
  const [apartment, setApartment] = useState(null);
  const { user } = useAuth();

  const isOwner = user && user.email === apartment.owner_email;

  useEffect(() => {
    api.get(`/apartments/${slug}/`)
      .then((res) => setApartment(res.data))
      .catch((err) => console.error("Ошибка загрузки деталей:", err));
  }, [slug]);

  if (!apartment) {
    return <div className="p-4">Загрузка...</div>;
  }

  const formatDate = (isoString) =>
    new Date(isoString).toLocaleString("ru-RU", {
      day: "2-digit",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const formatPrice = (value) =>
    new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "UAH",
      minimumFractionDigits: 2,
    }).format(value);

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <Link to="/" className="text-blue-600 hover:underline">
        ← Назад
      </Link>
      <h1 className="text-3xl font-bold mt-4">{apartment.name}</h1>
      <p className="mt-2 text-gray-600">{apartment.description}</p>
      <p className="mt-4">Количество комнат: {apartment.number_of_rooms}</p>
      <p className="mt-1">Площадь: {apartment.square} кв. м</p>
      <p className="mt-1">Цена: {formatPrice(apartment.price)}</p>
      <p className="mt-1">Дата создания: {formatDate(apartment.created_at)}</p>
      <p className="mt-1">Дата обновления: {formatDate(apartment.updated_at)}</p>
      <p className='mt-1'>Владелец: {apartment.owner_email}</p>
      <p className="mt-2">
        Статус:{" "}
        {apartment.availability ? (
          <span className="text-green-600">Доступна</span>
        ) : (
          <span className="text-red-600">Недоступна</span>
        )}
      </p>
      <div className="mt-8">
        {isOwner && (
          <Link
          to={`/apartments/${apartment.slug}/edit`}
          className="inline-block mt-4 bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
          >
           Редактировать
          </Link>
        )}
      </div>
    </div>
    );
};

export default ApartmentDetail;
