package main

import (
	"encoding/json"
	"bytes"
	"io"
	"log"
	"net/http"
	"github.com/rs/cors"
)

type PredictionRequest struct {
	Gender           int     `json:"Gender"`
	Age              int     `json:"Age"`
	GPA              float64 `json:"GPA"`
	InterestedDomain int     `json:"Interested Domain"` // Ensure this matches "Interested Domain" in frontend
	Projects         int     `json:"Projects"`
	Average          int     `json:"Average"`
	Strong           int     `json:"Strong"`
	Weak             int     `json:"Weak"`
	SQL_Average      int     `json:"SQL_Average"`
	SQL_Strong       int     `json:"SQL_Strong"`
	SQL_Weak         int     `json:"SQL_Weak"`
	Java_Average     int     `json:"Java_Average"`
	Java_Strong      int     `json:"Java_Strong"`
	Java_Weak        int     `json:"Java_Weak"`
}

type PredictionResponse struct {
	PredictedCareer string `json:"predicted_career"`
}

func handlePrediction(w http.ResponseWriter, r *http.Request) {
	var requestData PredictionRequest

	// Decode JSON request body
	if err := json.NewDecoder(r.Body).Decode(&requestData); err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	// Log the request to ensure it's received correctly
	log.Printf("Received data: %+v", requestData)

	// Here you would call your machine learning model to predict the career
	// For now, returning a dummy response
	jsonData, err := json.Marshal(requestData)
	if err != nil {
		log.Fatalf("Error marshaling request data: %v", err)
	}

	// Set up the request to the Flask API
	url := "http://localhost:5000/predict"
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatalf("Error making request to Flask service: %v", err)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response from Flask service: %v", err)
	}
	var predictionResponse PredictionResponse
	if err := json.Unmarshal(body, &predictionResponse); err != nil {
		log.Fatalf("Error unmarshaling response JSON: %v", err)
	}

	// Print the prediction result
	log.Printf("Predicted Career: %s\n", predictionResponse.PredictedCareer)
	// Respond with the predicted career
	response := PredictionResponse{
		PredictedCareer: predictionResponse.PredictedCareer,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// CORS middleware options
	c := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedMethods: []string{"GET", "POST", "OPTIONS"},
		AllowedHeaders: []string{"Content-Type"},
		AllowCredentials: true,
		MaxAge: 3600,
	})

	// Create a handler and wrap it with CORS middleware
	handler := http.NewServeMux()
	handler.HandleFunc("/predict", handlePrediction)

	// Start the server with CORS middleware
	log.Println("Starting server on http://localhost:8080...")
	log.Fatal(http.ListenAndServe(":8080", c.Handler(handler)))
}
