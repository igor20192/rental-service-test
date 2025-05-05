import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

const ApartmentCreateForm = () => {
  const [form, setForm] = useState({
    name: "",
    description: "",
    number_of_rooms: 1,
    square: "",
    price: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/apartments/", form, { withCredentials: true });
      navigate("/"); 
    } catch (error) {
      console.error("Ошибка при создании:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Создать квартиру</h2>
      {["name", "description", "square", "price"].map((field) => (
        <input
          key={field}
          name={field}
          placeholder={field}
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
        placeholder="Количество комнат"
        className="block w-full mb-3 p-2 border rounded"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Создать
      </button>
    </form>
  );
};

export default ApartmentCreateForm;
