

import * as ReactDOM from "react-dom/client";
import Homepage from "./screen/homepage/homepage";
import Chat from "./screen/chat/chat";
import Farmdata from "./screen/farm-data/farm-data";


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
  {
    path: "/dashboard/farm-data",
    element: <Farmdata/>,
  },
]);

function App() {
  return (
    <RouterProvider router={ router} />
  );
}

export default App;
