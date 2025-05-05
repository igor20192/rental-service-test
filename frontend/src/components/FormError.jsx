const FormError = ({ error }) => {
    if (!error) return null;
  
    return <p className="text-red-600 text-sm mt-1">{error}</p>;
  };
  
  export default FormError;
  