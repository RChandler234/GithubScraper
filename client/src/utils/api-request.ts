class ServerError extends Error {
  status_code: number;
  error: string;

  constructor(status_code: number, error: string) {
    super(error);
    this.status_code = status_code;
    this.error = error;
  }
}

export const sendAPIRequest = async (url: string) => {
  const response = await fetch(url);

  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new ServerError(errorData.status_code, errorData.error);
    } catch (e: unknown) {
      if (e instanceof ServerError) {
        throw new Error(`Error (${e.status_code}): ${e.error}`);
      }
      throw new Error(`Error: Internal Server Error`);
    }
  }

  const data = await response.json();

  return data;
};
