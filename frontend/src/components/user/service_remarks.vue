<template>
    <div class="remarks-container">
        <h2>Service Remarks for "{{ service.service_name }}"</h2>
        <div class="info">
            <p><strong>Request ID:</strong> {{ service.id }}</p>
            <p><strong>Service Name:</strong> {{ service.service_name }}</p>
            <p><strong>Professional Name:</strong> {{ service.professional_name }}</p>
            <p><strong>Professional Phone:</strong> {{ service.professional_phone }}</p>
            <p><strong>Date of Request:</strong> {{ service.date_of_request }}</p>
            <p><strong>Status:</strong> {{ service.service_status }}</p>
            <p><strong>Remarks:</strong> {{ service.remarks }}</p>
        </div>

        <div class="review-section">
            <label for="rating">Rate this service:</label>
            <select v-model="rating" id="rating" class="rating-select">
                <option value="1">1 Star</option>
                <option value="2">2 Stars</option>
                <option value="3">3 Stars</option>
                <option value="4">4 Stars</option>
                <option value="5">5 Stars</option>
            </select>

            <label for="comments">Add your review:</label>
            <textarea v-model="comments" id="comments" rows="4" placeholder="Write your review here..." class="review-textarea" maxlength="200"></textarea>
            <div class="char-count">{{ remainingChars }} characters remaining</div>

            <button @click="submitReview" class="submit-button">Submit Review</button>
            <button @click="$emit('close')" class="close-button">Close</button>
        </div>
    </div>
</template>

<script>
import customerService from '@/services/customerService'; // Import the customer service

export default {
    props: {
        service: Object // Receive the service object as a prop
    },
    data() {
        return {
            rating: 1, // Default rating
            comments: '' // Review comments
        };
    },
    computed: {
        remainingChars() {
            return 200 - this.comments.length; // Calculate remaining characters
        }
    },
    methods: {
        async submitReview() {
            const token = localStorage.getItem('token'); // Get the token from localStorage
            if (!token) {
                alert('You are not logged in. Please log in to submit a review.'); // Alert if token is not found
                return; // Exit the method if no token is found
            }
            try {
                // Convert rating to an integer before sending
                const numericRating = parseInt(this.rating, 10); // Convert rating to an integer

                // Call the submitReview API with the request ID and review data
                const response = await customerService.submitReview(this.service.id, {
                    rating: numericRating, // Use the numeric rating
                    comments: this.comments
                });
                alert(response.data.message); // Show success message
                this.$emit('close'); // Close the remarks component after submission
            } catch (error) {
                console.error('Error submitting review:', error); // Log the error
                alert('An error occurred while submitting the review.'); // Show a generic error message
            }
        }
    }
};
</script>

<style scoped>
.remarks-container {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    background-color: #190228;
    margin-top: 20px;
    color: #fff; /* Text color */
    max-width: 600px; /* Set a maximum width */
    margin-left: auto; /* Center the component */
    margin-right: auto; /* Center the component */
}

.info {
    margin-bottom: 20px; /* Space between info and review section */
}

.review-section {
    display: flex;
    flex-direction: column; /* Stack elements vertically */
}

.rating-select {
    margin-bottom: 10px; /* Space below the rating select */
}

.review-textarea {
    margin-bottom: 10px; /* Space below the textarea */
    padding: 10px; /* Padding inside the textarea */
    border-radius: 5px; /* Rounded corners */
    border: 1px solid #ccc; /* Border style */
    resize: none; /* Disable resizing */
}

.char-count {
    font-size: 12px; /* Smaller font for character count */
    color: #ccc; /* Light color for character count */
    margin-bottom: 10px; /* Space below character count */
}

.submit-button, .close-button {
    padding: 10px 15px; /* Padding for buttons */
    border: none; /* Remove border */
    border-radius: 5px; /* Rounded corners */
    cursor: pointer; /* Pointer cursor on hover */
    margin-right: 10px; /* Space between buttons */
}

.submit-button {
    background-color: #007bff; /* Button color */
    color: white; /* Text color */
}

.submit-button:hover {
    background-color: #0056b3; /* Darker shade on hover */
}

.close-button {
    background-color: #ccc; /* Close button color */
    color: black; /* Text color */
}

.close-button:hover {
    background-color: #aaa; /* Darker shade on hover */
}
</style>