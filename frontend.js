document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Show the loading GIF
    const loadingDiv = document.getElementById('loading');
    loadingDiv.classList.remove('hidden'); // Show loading

    // Collect form data
    const formData = new FormData(this);
    const data = {
        Gender: parseInt(formData.get('Gender')),
        Age: parseInt(formData.get('Age')),
        GPA: parseFloat(formData.get('GPA')),
        "Interested Domain": parseInt(formData.get('Interested Domain')),
        Projects: parseInt(formData.get('Projects')),
        Average: formData.get('GeneralSkill') === 'Average' ? 1 : 0,
        Strong: formData.get('GeneralSkill') === 'Strong' ? 1 : 0,
        Weak: formData.get('GeneralSkill') === 'Weak' ? 1 : 0,
        SQL_Average: formData.get('SQLSkill') === 'Average' ? 1 : 0,
        SQL_Strong: formData.get('SQLSkill') === 'Strong' ? 1 : 0,
        SQL_Weak: formData.get('SQLSkill') === 'Weak' ? 1 : 0,
        Java_Average: formData.get('JavaSkill') === 'Average' ? 1 : 0,
        Java_Strong: formData.get('JavaSkill') === 'Strong' ? 1 : 0,
        Java_Weak: formData.get('JavaSkill') === 'Weak' ? 1 : 0
    };

    // Send data to Go backend
    fetch('http://localhost:8080/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const resultDiv = document.getElementById('result');
        
        // Hide the loading GIF
        loadingDiv.classList.add('hidden'); // Hide loading GIF

        // Display the predicted careers
        let careerHtml = `<h1 style="text-decoration: underline;">Predicted Careers:</h1>`;
        result.predicted_career.forEach((career, index) => {
            careerHtml += `<h3>${index + 1}. ${career}</h3>`;
        });

        resultDiv.innerHTML = careerHtml;
        resultDiv.classList.remove('hidden');
        resultDiv.classList.add('fade-in');
    })
    .catch(error => {
        console.error('Error:', error);

        // Hide the loading GIF if there's an error
        loadingDiv.classList.add('hidden');
    });
});


// Data for dropdowns
const projects = [
    '3D Animation', '3D Modeling', '3D Rendering', 'AWS Deployment', 'Android App',
    'Android App Development', 'Android Game', 'Big Data Analytics', 'Chatbot Development',
    'Cloud Infrastructure Management', 'Cloud Migration Specialist', 'Cloud Solution Architecture',
    'Computer Forensic Analyst', 'Computer Vision', 'Cross-Platform App Development',
    'Data Analytics', 'Data Mining', 'Data Warehouse Design', 'Deep Learning Models', 'DevOps',
    'Distributed Systems Architect', 'E-commerce Website', 'Embedded Systems',
    'Enterprise Software Development', 'Firewall Management', 'Front-End Development',
    'Full-Stack Web App', 'GCP Deployment', 'GIS Mapping', 'Game Development',
    'Genomic Data Analysis', 'Healthcare Data Analyst', 'Image Classification',
    'Image Recognition', 'Machine Learning', 'Market Analysis', 'Medical Imaging Analysis',
    'Mobile App Development', 'Mobile Game Development', 'Natural Language Processing',
    'Network Security', 'Neural Network Development', 'Object Detection', 'Penetration Testing',
    'Privacy Compliance Officer', 'Protein Structure Prediction', 'Quantum Algorithm Development',
    'Reinforcement Learning', 'Robotics', 'SQL Database Administration', 'SQL Database Design',
    'SQL Query Optimization', 'Search Engine Optimization', 'Security Auditing',
    'Smart Contracts Developer', 'Smart Home Automation', 'Social Media Platform',
    'Statistical Analysis', 'Usability Testing', 'User Experience Researcher',
    'Virtual Reality Development', 'Web Application Development', 'iOS App',
    'iOS App Development', 'iOS Game'
];

const domains = [
    'Artificial Intelligence', 'Bioinformatics', 'Biomedical Computing',
    'Blockchain Technology', 'Cloud Computing', 'Computer Graphics',
    'Computer Vision', 'Cybersecurity', 'Data Mining', 'Data Privacy',
    'Data Science', 'Database Management', 'Digital Forensics',
    'Distributed Systems', 'Game Development', 'Geographic Information Systems',
    'Human-Computer Interaction', 'Information Retrieval', 'IoT (Internet of Things)',
    'Machine Learning', 'Mobile App Development', 'Natural Language Processing',
    'Network Security', 'Quantum Computing', 'Software Development',
    'Software Engineering', 'Web Development'
];

// Utility to populate a dropdown
function populateDropdown(dropdownId, items) {
    const dropdown = document.getElementById(dropdownId);
    items.forEach((item, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = item;
        dropdown.appendChild(option);
    });
}

// Populate dropdowns on page load
document.addEventListener('DOMContentLoaded', () => {
    populateDropdown('domain', domains);
    populateDropdown('projects', projects);
});
