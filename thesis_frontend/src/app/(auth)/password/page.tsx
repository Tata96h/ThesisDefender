"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import '../../(landing-page)/landingpage-style.css';
import AlertMessage from '@/components/AlertMessage/page';


const Password = () => {
  const router = useRouter();
  const [treatment, setTreatment] = useState(false);
  const [message, setMessage] = useState("");
  const [styleMessage, setStyleMessage] = useState("");
 const [messageType, setMessageType] = useState<"success" | "error" | undefined>(undefined); 
  const [passwordconfirm, setPasswordconfirm] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem("isload", "0");
      const session = localStorage.getItem("sessionIsActive");
      if (session === "1") {
        router.push('/');
      }
    }
  }, [router]);

  const handlePassword = async (e) => {
    e.preventDefault();
    setTreatment(true);
    setMessageType("success");
    setMessage("Traitement...");

    if (!passwordconfirm || !password) {
    setMessageType("error");
      setMessage("Tous les champs sont obligatoires !!");
      return;
    }

    const formData = {
      passwordconfirm: passwordconfirm,
      password: password,
    };

    try {
      const response = await fetch("", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        cache: "no-store"
      });

      const responseData = await response.json();
      console.log(responseData);

      if (response.ok) {
         if (typeof window !== 'undefined') {
        //   localStorage.setItem("accessToken", responseData.access_token);
        //   localStorage.setItem("tokenType", responseData.token_type);
        //   localStorage.setItem(
        //     "userInfo",
        //     JSON.stringify(responseData.user_info)
        //   );
        //   localStorage.setItem("sessionIsActive", "1");
          router.push("/login");
        }
      } else {
        // const errorData = await response.json();
      setMessageType("error");
      setMessage(`Échec de l´authentification`);

        // setError(`Échec de la connexion : ${errorData.message || response.status}`);
      }
    } catch (error) {
      setMessageType("error");
      setMessage("Ces identifiants n'existent pas");
    }
  };

  return (
    <div className="font-[sans-serif] text-[#333]">
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="grid md:grid-cols-2 items-center gap-4 max-w-6xl w-full p-4 m-4 shadow-[0_2px_10px_-3px_rgba(6,81,237,0.3)] rounded-md">
          <div className="md:max-w-md w-full sm:px-6 py-4">
            <form onSubmit={handlePassword}>
              <div className="mb-12">
                <h3 className="text-3xl font-extrabold">Authentification </h3>
              </div>
               {message && <AlertMessage type={messageType || 'success'} message={message} />}

              {/* {treatment ? (
                <div className={"text-center " + messageType}>
                  {" "}
                  {message}{" "}
                </div>
              ) : (
                ""
              )}
              {error && <p>{error}</p>} */}
              
              <div className="mt-8">
                <label className="text-xs block mb-2">Mot de passe</label>
                <div className="relative flex items-center">
                  <input
                    name="password"
                    type="password"
                    className="w-full text-sm border-b border-gray-300 focus:border-[#333] px-2 py-3 outline-none"
                    placeholder="Entrez votre mot de passe"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="#bbb"
                    stroke="#bbb"
                    className="w-[18px] h-[18px] absolute right-2 cursor-pointer"
                    viewBox="0 0 128 128"
                  >
                    {/* SVG code */}
                  </svg>
                </div>
              </div>
              <div className="mt-8">
                <label className="text-xs block mb-2">Mot de passe confirmé</label>
                <div className="relative flex items-center">
                  <input
                    name="passwordconfirm"
                    type="password"
                    className="w-full text-sm border-b border-gray-300 focus:border-[#333] px-2 py-3 outline-none"
                    placeholder="Confirmez votre mot de passe"
                    value={passwordconfirm}
                    onChange={(e) => setPasswordconfirm(e.target.value)}
                  />
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="#bbb"
                    stroke="#bbb"
                    className="w-[18px] h-[18px] absolute right-2 cursor-pointer"
                    viewBox="0 0 128 128"
                  >
                    {/* SVG code */}
                  </svg>
                </div>
              </div>
             
              <div className="mt-12">
                <button
                  type="submit"
                  className="w-full shadow-xl py-2.5 px-4 text-sm font-semibold rounded-full text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
                >
                  Valider
                </button>
              </div>
              
            </form>
          </div>
          <div className="md:h-full w-full max-md:mt-10 bg-white rounded-xl lg:p-12 p-8">
            <Image
              src="/images/login/imgLogin.png"
              alt="nothing"
              width={1000}
              height={1}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Password;
