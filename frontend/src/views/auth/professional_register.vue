<template>
    
    <div class="register-container">
        
        <form class="register-form" @submit.prevent="registerProfessional">
            <h1>Register as a Professional</h1>
            <input v-model="professional.fullname" placeholder="Full Name" required />
            <input v-model="professional.email" type="email" placeholder="Email" required />
            <input v-model="professional.username" placeholder="Username" required />
            <input v-model="professional.password" type="password" placeholder="Password" required />
 

            <select v-model="professional.service_name" required>
                <option value="" disabled>Select a service</option>
                <option v-for="service in services" :key="service.id" :value="service.name">
                    {{ service.name }}
                </option>
            </select>

            <select v-model="professional.experience" required>
                <option value="0" >Less than 1 year</option>
                <option v-for="year in experienceYears" :key="year" :value="year">
                    {{ year }} years
                </option>
                <option value="99" >10+ years</option>
            </select>
            


            <input v-model="professional.phone" type="tel" placeholder="Phone" required />
            <input v-model="professional.address" placeholder="Address" />
            <input v-model="professional.pincode" placeholder="Pincode" />
            <button type="submit">Register</button>
            <p v-if="message">{{ message }}</p>
            <router-link to="/login"> Back to Login</router-link>
        </form>
        
    </div>
    
</template>

<script>
import authService from '@/services/authService';
import professionalService from '@/services/professionalService'; 
export default {
    data() {
        return {
            professional: {
                fullname: '',
                email: '',
                username: '',
                password: '',
                service_name: '',
                experience: null,
                phone: '',
                address: '',
                pincode: '',
            },
            services:[],
            message: '',
            experienceYears: Array.from({ length: 10 }, (_, i) => i + 1),
        };
    },

    created() {
        this.fetchServices(); // Fetch services when the component is created
    },


    methods: {
        async fetchServices() {
            try {
                this.services = await professionalService.getServices(); // Fetch services using the service file
            } catch (error) {
                console.error('Error fetching services:', error);
            }
        },
        async registerProfessional() {
            try {
                const response = await authService.registerProfessional(this.professional);
                this.message = response.message; // Display success message
            } catch (error) {
                this.message = error.message; // Display error message
            }
        },




    },
};
</script>

<style>
html, body {
  background-color: black;
  height: 100%;
  margin: 0;
  padding: 0;
}

.register-container {
  margin-top:50px;
  margin-left: 30%;
  align-items: center;
  width: 40%;  
  height: 100%; 
  padding: 20px; 
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px 5px rgb(144, 86, 221);
}

.register-form {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px 5px rgba(144, 86, 221, 0.5);
  color: white;
}

.form-group {
  margin-bottom: 15px;
}



.register-form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: none;
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  transition: box-shadow 0.3s ease;
}

.register-form input::placeholder {
  color: rgb(255, 255, 255); /* Lighter color for placeholder text */
}

.register-form input:focus {
  outline: none;
  box-shadow: 0 0 10px 2px rgba(144, 86, 221, 0.8);
}

.register-form button {
  width: 100%;
  padding: 10px;
  background-color: rgb(144, 86, 221);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.register-form button:hover {
  background-color: rgba(237, 82, 237, 0.8);
}
</style>