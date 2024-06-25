"use client";

import { useState } from 'react';
import Head from 'next/head';

export default function StudentSpace() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [file, setFile] = useState(null);
  const [theme, setTheme] = useState('');
  const [profile, setProfile] = useState({
    name: 'Jean Dupont',
    email: 'jean.dupont@email.com',
    avatar: 'https://via.placeholder.com/150',
  });

  const handleFileChange = (e) => setFile(e.target.files[0]);
  const handleThemeChange = (e) => setTheme(e.target.value);
  const handleProfileChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const NavBar = () => (
    <nav className="bg-gradient-to-r from-purple-500 to-indigo-600 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">EspacEtudiant</h1>
        <div className="flex space-x-4">
          {['Dashboard', 'Mémoire', 'Thème', 'Profil'].map((item) => (
            <button
              key={item}
              onClick={() => setActiveTab(item.toLowerCase())}
              className={`px-3 py-2 rounded-full transition-colors duration-300 ${
                activeTab === item.toLowerCase()
                  ? 'bg-white text-purple-600'
                  : 'hover:bg-purple-400'
              }`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );

  const Footer = () => (
    <footer className="bg-gray-800 text-white p-4 mt-8">
      <div className="container mx-auto text-center">
        <p>&copy; 2024 EspacEtudiant. Tous droits réservés.</p>
      </div>
    </footer>
  );

  const Dashboard = () => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Bienvenue, {profile.name}!</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-100 p-4 rounded-lg">
          <h3 className="font-bold text-lg mb-2">Statut du mémoire</h3>
          <p>En attente de dépôt</p>
        </div>
        <div className="bg-green-100 p-4 rounded-lg">
          <h3 className="font-bold text-lg mb-2">Statut du thème</h3>
          <p>Non soumis</p>
        </div>
      </div>
    </div>
  );

  const Profile = () => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Profil</h2>
      <div className="flex items-center mb-4">
        <img src={profile.avatar} alt="Avatar" className="w-24 h-24 rounded-full mr-4" />
        <div>
          <input
            type="text"
            name="name"
            value={profile.name}
            onChange={handleProfileChange}
            className="block w-full p-2 mb-2 border rounded"
          />
          <input
            type="email"
            name="email"
            value={profile.email}
            onChange={handleProfileChange}
            className="block w-full p-2 border rounded"
          />
        </div>
      </div>
      <button className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded">
        Sauvegarder les modifications
      </button>
    </div>
  );

  const UploadThesis = () => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Déposer le mémoire</h2>
      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
        />
      </div>
      <button className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded">
        Envoyer le mémoire
      </button>
    </div>
  );

  const SubmitTheme = () => (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">Soumettre le thème</h2>
      <textarea
        value={theme}
        onChange={handleThemeChange}
        className="w-full p-2 mb-4 border rounded"
        rows="4"
        placeholder="Entrez votre thème ici..."
      ></textarea>
      <button className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded">
        Soumettre le thème
      </button>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Head>
        <title>EspacEtudiant</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <NavBar />

      <main className="flex-grow container mx-auto p-4">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'mémoire' && <UploadThesis />}
        {activeTab === 'thème' && <SubmitTheme />}
        {activeTab === 'profil' && <Profile />}
      </main>

      <Footer />
    </div>
  );
}