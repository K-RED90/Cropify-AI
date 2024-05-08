

import * as ReactDOM from "react-dom/client";
import Homepage from "./screen/homepage/homepage";
import Chat from "./screen/chat/chat";
import Farmdata from "./screen/farm-data/farm-data";
import Control from "./screen/control/control";
import AddPicture from "./screen/add-picture/add-pic";

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
    path: "/dashboard",
    element: <Chat/>,
  },
  {
    path: "/dashboard/farm-data",
    element: <Farmdata/>,
  },
  {
    path: "/dashboard/image",
    element: <AddPicture/>,
  },
  {
    path: "/dashboard/control",
    element: <Control/>,
  },
]);

function App() {
  return (
    <RouterProvider router={ router} />
  );
}

export default App;
