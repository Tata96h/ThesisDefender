// import { Icons } from "@/components/icons";
// import { NavItem, SidebarNavItem } from "@/types";



export type Etudian = {
  id: number;
  username: string;
  nom: string;
  prenoms: string;
  filiere_id: number;
  annee_id: number;
  grade_id: number;
  email: string;
  bio: string;
};
export type Enseignan = {
  id: number;
  username: string;
  nom: string;
  prenoms: string;
  departement_id: string;
  annee_id: number;
  grade_id: number;
  email: string;
  bio: string;
};

