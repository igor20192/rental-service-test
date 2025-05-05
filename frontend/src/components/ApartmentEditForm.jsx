import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";

const ApartmentEditForm = () => {
  const { slug } = useParams();
  const [form, setForm] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`/apartments/${slug}/`).then((res) => setForm(res.data));
  }, [slug]);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/apartments/${slug}/`, form, { withCredentials: true });
      navigate(`/apartments/${slug}`);
    } catch (err) {
      console.error("Ошибка при сохранении:", err);
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Удалить квартиру?")) {
      try {
        await api.delete(`/apartments/${slug}/`, { withCredentials: true });
        navigate("/");
      } catch (err) {
        console.error("Ошибка при удалении:", err);
      }
    }
  };

  if (!form) return <div>Загрузка...</div>;

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Редактировать</h2>
      {["name", "description", "square", "price"].map((field) => (
        <input
          key={field}
          name={field}
          value={form[field]}
          onChange={handleChange}
          className="block w-full mb-3 p-2 border rounded"
        />
      ))}
      <input
        type="number"
        name="number_of_rooms"
        value={form.number_of_rooms}
        onChange={handleChange}
        className="block w-full mb-3 p-2 border rounded"
      />
      <button type="submit" className="bg-green-600 text-white px-4 py-2 mr-4 rounded">
        Сохранить
      </button>
      <button type="button" onClick={handleDelete} className="bg-red-600 text-white px-4 py-2 rounded">
        Удалить
      </button>
    </form>
  );
};

export default ApartmentEditForm;
