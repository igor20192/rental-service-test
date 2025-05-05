import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";

const ApartmentEditForm = () => {
  const { slug } = useParams();
  const [form, setForm] = useState(null);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`/apartments/${slug}/`).then((res) => setForm(res.data));
  }, [slug]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    setErrors({ ...errors, [name]: null }); // сбрасываем ошибку при вводе
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    try {
      await api.put(`/apartments/${slug}/`, form, { withCredentials: true });
      navigate(`/apartments/${slug}`);
      alert("Квартира успешно отредактирована!");
    } catch (err) {
      if (err.response?.status === 400) {
        setErrors(err.response.data);
      } else {
        console.error("Ошибка при сохранении:", err);
        alert("Ошибка при сохранении. Попробуйте позже.");
      }
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Удалить квартиру?")) {
      try {
        await api.delete(`/apartments/${slug}/`, { withCredentials: true });
        navigate("/");
      } catch (err) {
        console.error("Ошибка при удалении:", err);
        alert("Ошибка при удалении.");
      }
    }
  };

  if (!form) return <div>Загрузка...</div>;

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Редактировать</h2>

      {["name", "description", "square", "price"].map((field) => (
        <div key={field} className="mb-3">
          <input
            name={field}
            value={form[field]}
            onChange={handleChange}
            className="block w-full p-2 border rounded"
            placeholder={field}
          />
          {errors[field] && (
            <p className="text-red-600 text-sm mt-1">{errors[field]}</p>
          )}
        </div>
      ))}

      <div className="mb-4">
        <input
          type="number"
          name="number_of_rooms"
          value={form.number_of_rooms}
          onChange={handleChange}
          className="block w-full p-2 border rounded"
          placeholder="Количество комнат"
        />
        {errors.number_of_rooms && (
          <p className="text-red-600 text-sm mt-1">{errors.number_of_rooms}</p>
        )}
      </div>

      <button type="submit" className="bg-green-600 text-white px-4 py-2 mr-4 rounded">
        Сохранить
      </button>
      <button
        type="button"
        onClick={handleDelete}
        className="bg-red-600 text-white px-4 py-2 rounded"
      >
        Удалить
      </button>
    </form>
  );
};

export default ApartmentEditForm;
