// --- CONFIGURAÇÃO DO FIREBASE ---
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";

// CONFIG DO SEU FIREBASE
const firebaseConfig = {
  apiKey: "SUA_API_KEY",
  authDomain: "SEU_AUTH_DOMAIN",
  projectId: "SEU_PROJECT_ID",
  storageBucket: "SEU_BUCKET",
  messagingSenderId: "SEU_ID",
  appId: "SEU_APP"
};

// Inicializa Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// --- LOGIN ---
const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;

  try {
    // Login no Auth
    const userCredential = await signInWithEmailAndPassword(auth, email, senha);
    const user = userCredential.user;

    // Verifica tipo do usuário
    const userType = await verificarTipoUsuario(user.uid);

    if (!userType) {
      alert("Seu login está correto, mas seu perfil não foi encontrado no banco.");
      return;
    }

    // Redirecionamentos
    if (userType === "loja") {
      window.location.href = "home_loja.html";
    } 
    else if (userType === "revendedora") {
      window.location.href = "home_revendedora.html";
    }
    else if (userType === "admin") {
      window.location.href = "admin_dashboard.html";
    }

  } catch (error) {
    console.log(error);
    alert("Email ou senha incorretos.");
  }
});

// --- VERIFICA O TIPO DO USUÁRIO ---
async function verificarTipoUsuario(uid) {
  // Caminhos das coleções
  const colecoes = [
    { nome: "Lojas", tipo: "loja" },
    { nome: "Revendedoras", tipo: "revendedora" },
    { nome: "Admins", tipo: "admin" }
  ];

  // Procurar o UID em cada coleção
  for (let col of colecoes) {
    const ref = doc(db, col.nome, uid);
    const docSnap = await getDoc(ref);

    if (docSnap.exists()) {
      // Retorna o tipo correspondente
      return col.tipo;
    }
  }

  // Se não encontrou em nenhuma
  return null;
}
