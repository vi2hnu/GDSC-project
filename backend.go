package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
)

// Define a struct to represent the prediction request payload
type PredictionRequest struct {
    Gender           int     `json:"Gender"`
    Age              int     `json:"Age"`
    GPA              float64 `json:"GPA"`
    InterestedDomain int     `json:"Interested Domain"`
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

// Define a struct to handle the prediction response from the Flask API
type PredictionResponse struct {
    PredictedCareer string `json:"predicted_career"`
}

func main() {
    // Create a sample prediction request payload
    requestData := PredictionRequest{
        Gender:           0,
        Age:              21,
        GPA:              3.7,
        InterestedDomain: 26,
        Projects:         1,
        Average:          0,
        Strong:           0,
        Weak:             1,
        SQL_Average:      0,
        SQL_Strong:       1,
        SQL_Weak:         0,
        Java_Average:     0,
        Java_Strong:      1,
        Java_Weak:        0,
    }

    // Convert the requestData struct to JSON
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

    // Read the response from the Flask API
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Fatalf("Error reading response from Flask service: %v", err)
    }

    // Parse the JSON response
    var predictionResponse PredictionResponse
    if err := json.Unmarshal(body, &predictionResponse); err != nil {
        log.Fatalf("Error unmarshaling response JSON: %v", err)
    }

    // Print the prediction result
    fmt.Printf("Predicted Career: %s\n", predictionResponse.PredictedCareer)
}
