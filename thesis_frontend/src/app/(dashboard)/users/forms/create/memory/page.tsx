"use client";
import { useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import AlertMessage from "@/components/AlertMessage/page";

const DepotMemoire = () => {
  const [messageType, setMessageType] = useState<"success" | "error" | undefined>(undefined);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    binome1: "",
    binome2: "",
    theme: "",
    dateHeureDepot: "",
    fichierMemoire: null,
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleFileChange = (event) => {
    setFormData((prevState) => ({
      ...prevState,
      fichierMemoire: event.target.files[0],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.binome1 || !formData.binome2 || !formData.theme || !formData.dateHeureDepot || !formData.fichierMemoire) {
      setMessageType("error");
      setMessage("Tous les champs sont obligatoires !");
      return;
    }

    try {
      const formDataToSend = new FormData();
      for (const key in formData) {
        formDataToSend.append(key, formData[key]);
      }

      const response = await fetch("http://127.0.0.1:8000/memoires/depot/", {
        method: "POST",
        body: formDataToSend,
      });

      if (response.ok) {
        setMessageType("success");
        setMessage("Dépôt de mémoire effectué avec succès !");
        // Réinitialiser le formulaire ou rediriger
      } else {
        setMessageType("error");
        setMessage(`Échec du dépôt : ${response.statusText}`);
      }
    } catch (error) {
      setMessageType("error");
      setMessage(`Une erreur est survenue lors du dépôt : ${error.message}`);
    }
  };

  return (
    <DefaultLayout>
      <div className="flex justify-center pt-20">
        <div className="w-full max-w-4xl px-4">
          <div className="flex flex-col gap-9">
            <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
              <div className="border-b border-stroke px-6.5 py-4 dark:border-strokedark mb-3">
                <h3 className="font-medium text-blue-500 dark:text-white">
                  Dépôt de Mémoire
                </h3>
                <div className="mt-5">
                  {message && <AlertMessage type={messageType || 'success'} message={message} />}
                </div>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="p-6.5">
                  <div className="mb-4.5">
                    <label className="mb-2.5 block text-black dark:text-white">
                      Binôme 1
                    </label>
                    <input
                      type="text"
                      name="binome1"
                      placeholder="Nom du premier membre du binôme"
                      className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                      onChange={handleInputChange}
                    />
                  </div>

                  <div className="mb-4.5">
                    <label className="mb-2.5 block text-black dark:text-white">
                      Binôme 2
                    </label>
                    <input
                      type="text"
                      name="binome2"
                      placeholder="Nom du second membre du binôme"
                      className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                      onChange={handleInputChange}
                    />
                  </div>

                  <div className="mb-4.5">
                    <label className="mb-2.5 block text-black dark:text-white">
                      Thème du mémoire
                    </label>
                    <input
                      type="text"
                      name="theme"
                      placeholder="Entrez le thème du mémoire"
                      className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                      onChange={handleInputChange}
                    />
                  </div>

                  <div className="mb-4.5">
                    <label className="mb-2.5 block text-black dark:text-white">
                      Date et heure de dépôt
                    </label>
                    <input
                      type="datetime-local"
                      name="dateHeureDepot"
                      className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                      onChange={handleInputChange}
                    />
                  </div>

                  <div className="mb-4.5">
                    <label className="mb-2.5 block text-black dark:text-white">
                      Fichier du mémoire
                    </label>
                    <input
                      type="file"
                      name="fichierMemoire"
                      accept=".pdf,.doc,.docx"
                      className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                      onChange={handleFileChange}
                    />
                  </div>

                  <button
                    type="submit"
                    className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray"
                  >
                    Déposer le mémoire
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default DepotMemoire;