export async function fetchData(url, method) {
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            const data = await response.json();
            return data; 
        }   
        return await response.json();
    }catch (error) {
        return {"Error": "Error fetching data"};
    }
}

