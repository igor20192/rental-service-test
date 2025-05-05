import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../contexts/AuthContext";


const ApartmentList = () => {
  const [apartments, setApartments] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");
  const [places, setPlaces] = useState("");
  const [availableOnly, setAvailableOnly] = useState(false);
  const [nextUrl, setNextUrl] = useState(null);
  const [prevUrl, setPrevUrl] = useState(null);
  const [currentUrl, setCurrentUrl] = useState("/apartments/");
  const { user } = useAuth();


  useEffect(() => {
    api.get(currentUrl)
      .then((response) => {
        setApartments(response.data.results);
        setNextUrl(response.data.next);
        setPrevUrl(response.data.previous);
      })
      .catch((err) => console.error("Ошибка при загрузке квартир:", err));
  }, [currentUrl]);

  useEffect(() => {
    let data = [...apartments];
    if (search) {
      data = data.filter(a =>
        a.name.toLowerCase().includes(search.toLowerCase()) ||
        a.description.toLowerCase().includes(search.toLowerCase())
      );
    }
    if (places) {
      data = data.filter(a => a.number_of_rooms >= parseInt(places));
    }
    if (availableOnly) {
      data = data.filter(a => a.availability);
    }
    setFiltered(data);
  }, [search, places, availableOnly, apartments]);

  const handleNext = () => {
    if (nextUrl) {
      const parsed = new URL(nextUrl);
      const path = parsed.pathname.replace("/api/v1/apartments/", "") + parsed.search;
      console.log(path);
      setCurrentUrl(`/apartments/${path}`);
      console.log(currentUrl);
    }
  };
  
  const handlePrev = () => {
    if (prevUrl) {
      const parsed = new URL(prevUrl);
      const path = parsed.pathname.replace("/api/v1", "") + parsed.search;
      setCurrentUrl(`${path}`);
    }
  };
  

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Квартиры</h1>
      <div className="mb-4">
      {user && (
        <Link
          to="/apartments/create"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          + Добавить квартиру
        </Link>
        )}
      </div>
      <div className="mb-6 flex flex-wrap gap-4">
        <input
          type="text"
          placeholder="Поиск по названию или описанию"
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border p-2 rounded w-full md:w-1/3"
        />
        <input
          type="number"
          placeholder="Мин. мест"
          value={places}
          onChange={e => setPlaces(e.target.value)}
          className="border p-2 rounded w-full md:w-1/6"
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={availableOnly}
            onChange={e => setAvailableOnly(e.target.checked)}
          />
          Только доступные
        </label>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {filtered.map(apartment => (
          <div
            key={apartment.id}
            className={`p-4 border rounded-lg shadow-sm transition ${
              apartment.availability ? "" : "opacity-50 blur-[1px]"
            }`}
          >
            <h2 className="text-xl font-semibold">{apartment.name}</h2>
            <p className="text-gray-600">{apartment.description}</p>
            <p className="mt-2">Количество комнат: {apartment.number_of_rooms}</p>
            <p className="mt-1">Площадь: {apartment.square} м²</p>
            <p className="mt-1">
              Статус:{" "}
              {apartment.availability ? (
                <span className="text-green-600">Доступна</span>
              ) : (
                <span className="text-red-600">Недоступна</span>
              )}
            </p>
            <Link
              to={`/apartments/${apartment.slug}`}
              className="mt-4 inline-block text-blue-600 hover:underline"
            >
              Подробнее
            </Link>
          </div>
        ))}
      </div>

      <div className="flex justify-between mt-8">
        <button
          onClick={handlePrev}
          disabled={!prevUrl}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          ← Назад
        </button>
        <button
          onClick={handleNext}
          disabled={!nextUrl}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Далее →
        </button>
      </div>
    </div>
  );
};

export default ApartmentList;
