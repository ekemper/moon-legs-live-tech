import { AppProvider } from './contexts/AppContext'
import { MainPage } from './components/MainPage'

export default function App() {
  return (
    <AppProvider>
      <MainPage />
    </AppProvider>
  )
}
