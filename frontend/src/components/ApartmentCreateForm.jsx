import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import FormError from "./FormError";


const ApartmentCreateForm = () => {
  const [form, setForm] = useState({
    name: "",
    description: "",
    number_of_rooms: 1,
    square: "",
    price: "",
  }); // Initialize form state with default values

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    setErrors({ ...errors, [name]: null }); // Clear error for the field on change
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({}); // Reset previous errors
    try {
      await api.post("/apartments/", form, { withCredentials: true });
      navigate("/");
      alert("Квартира успешно создана!");
    } catch (error) {
      if (error.response?.status === 400) {
        setErrors(error.response.data);
      } else { // Handle other errors
        console.error("Ошибка при создании:", error);
        alert("Произошла ошибка. Попробуйте позже.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Создать квартиру</h2> {/* "Create apartment" */}

      {["name", "description", "square", "price"].map((field) => (
        <div key={field} className="mb-3">
          <input
            name={field}
            placeholder={field}
            value={form[field]}
            onChange={handleChange}
            className="block w-full p-2 border rounded"
          />
          <FormError error={errors[field]} />
        </div>
      ))}

      <div className="mb-3">
        <input
          type="number"
          name="number_of_rooms"
          value={form.number_of_rooms}
          onChange={handleChange}
          placeholder="Количество комнат" // "Number of rooms" 
          className="block w-full p-2 border rounded"
        />
        <FormError error={errors.number_of_rooms} />
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Создать  
      </button>
    </form>
  );
};

export default ApartmentCreateForm;
