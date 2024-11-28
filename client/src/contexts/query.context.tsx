import { PropsWithChildren } from "react";
import { QueryClient, QueryClientProvider } from "react-query";

/**
 * Context to Provide QueryClient
 */
const QueryClientContext = (props: PropsWithChildren) => {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {props.children}
    </QueryClientProvider>
  );
};

export default QueryClientContext;
