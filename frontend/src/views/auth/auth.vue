<template>
  <div class="auth-container">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <input
          type="text"
          v-model="username"
          placeholder="Username"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
        />
      </div>
      <button type="submit" class="login-button">Login</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <div class="register-links">
        <router-link to="/register">Register as a Customer</router-link>
        <router-link to="/professional_register">Register as a Professional</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import authService from '/mad 2 housing/frontend/src/services/authService';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'Auth',
  setup() {
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const login = async () => {
      try {
        const { access_token, role } = await authService.login(username.value, password.value);
        localStorage.setItem('token', access_token);
        console.log(access_token);

        if (role === 'admin') {
          router.push('/admin_dashboard');
        } else if (role === 'professional') {
          router.push('/professional_dashboard');
        } else if (role === 'customer') {
          router.push('/user/homepage');
        }
      } catch (error) {
        errorMessage.value = error.message;
      }
    };

    return {
      username,
      password,
      errorMessage,
      login,
    };
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.register-links {
  text-align: center;
  margin-top: 20px;
}

.register-links a {
  margin: 0 10px;
  color: #007bff;
  text-decoration: none;
}

.register-links a:hover {
  text-decoration: underline;
}
</style>
