import { getToken } from "./auth"

export async function get(url) {
  const req = await fetch(url, {
    headers:{
      'Content-Type': 'application/json',
      'Authorization':`Bearer ${getToken()}`
    }
  })
  const res = await req.json()
  return res
}