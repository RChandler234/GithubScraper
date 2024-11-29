/**** Frontend Types **********/

export interface Project {
  userid: string;
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

/***** Backend Types */

export interface RequestBodyProject {
  userid: string;
  name: string;
  description: string;
  forks: number;
  stars: number;
  created_at: string;
  username: string;
}

export interface RequestBodyUser {
  username: string;
  created_at: string;
}
