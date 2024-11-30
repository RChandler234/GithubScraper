/**
 * Converts Datetime to String
 */
export const datetimePipe = (date: Date) => {
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
};
