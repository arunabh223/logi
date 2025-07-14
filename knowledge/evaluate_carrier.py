import pandas as pd

filepath = "knowledge/carrier_data.csv"

def create_carrier_scorecard(file_path: str) -> pd.DataFrame:
    """
    Create a carrier scorecard from the provided CSV file.
    Args:
        file_path (str): Path to the CSV file containing carrier data.
    Returns:
        pd.DataFrame: A DataFrame containing the carrier scorecard.
    """
    df = pd.read_csv(file_path)
    required_cols = ['CarrierName', 'OnTime', 'Damaged', 'CustomerRating']
    if not all(col in df.columns for col in required_cols):
        missing_cols = [col for col in required_cols if not col in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    scorecard = df[required_cols].copy()
    print("Historical data:\n",scorecard)

    # Convert 'OnTime' and 'Damaged' to boolean values 0 or 1
    for row in scorecard.index:
        scorecard.at[row, 'OnTime'] = 1 if scorecard.at[row, 'OnTime'] == 'Yes' else 0
        scorecard.at[row, 'Damaged'] = 1 if scorecard.at[row, 'Damaged'] == 'Yes' else 0

    # Calculate the final score
    for row in scorecard.index:
        scorecard.at[row, 'FinalScore'] = (
            scorecard.at[row, 'OnTime'] * 0.5 +
            (1 - scorecard.at[row, 'Damaged']) * 0.3 +
            scorecard.at[row, 'CustomerRating'] * 0.2
        )
    
    # Group by 'CarrierName' and calculate the average score
    scorecard = scorecard.drop(columns=['OnTime', 'Damaged', 'CustomerRating'])
    scorecard = scorecard.groupby('CarrierName').mean().reset_index()
    scorecard = scorecard.sort_values(by='FinalScore', ascending=False)
    return scorecard 

if __name__ == "__main__":
    scorecard = create_carrier_scorecard(filepath)
    print("\nScorecard:\n",scorecard)
    # Save the scorecard to a new CSV file
    scorecard.to_csv("knowledge/carrier_scorecard.csv", index=False)