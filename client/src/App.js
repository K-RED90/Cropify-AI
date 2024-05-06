

import * as ReactDOM from "react-dom/client";
import Homepage from "./screen/homepage/homepage";
import Chat from "./screen/chat/chat";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";


const router = createBrowserRouter([
  {
    path: "/",
    element: <Homepage/>,
  },

  {
    path: "/dashboard/chat",
    element: <Chat/>,
  },
]);

function App() {
  return (
    <RouterProvider router={ router} />
  );
}

export default App;
