/****************** Frontend Types *********************/

export interface Project {
  userId: string;
  name: string;
  description: string;
  forks: number;
  stars: number;
  createdAt: Date;
  username: string;
}

export interface User {
  username: string;
  createdAt: Date;
}

/************* Types for Data in Responses from API ********/

export interface APIResponseProject {
  user_id: string;
  name: string;
  description: string;
  forks: number;
  stars: number;
  created_at: string;
  username: string;
}

export interface APIResponseUser {
  username: string;
  created_at: string;
}
