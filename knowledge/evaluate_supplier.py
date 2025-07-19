import pandas as pd

filepath = "knowledge/supplier_data.csv"

def create_supplier_scorecard(file_path: str) -> pd.DataFrame:
    """
    Create a supplier scorecard from the provided CSV file.
    Args:
        file_path (str): Path to the CSV file containing supplier data.
    Returns:
        pd.DataFrame: A DataFrame containing the supplier scorecard.
    """
    df = pd.read_csv(file_path)
    
    required_cols = ['SupplierName', 'OnTimeDelivery', 'DefectRate', 'SupplierRating']
    if not all(col in df.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

    scorecard = df[required_cols].copy()
    print("Historical supplier data:\n", scorecard)

    # Convert 'OnTimeDelivery' and 'DefectRate' to numerical values
    for row in scorecard.index:
        scorecard.at[row, 'OnTimeDelivery'] = 1 if scorecard.at[row, 'OnTimeDelivery'] == 'Yes' else 0
        scorecard.at[row, 'DefectRate'] = 1 if scorecard.at[row, 'DefectRate'] == 'High' else 0  # assuming 'High' = 1, 'Low' = 0

    # Calculate the final score
    for row in scorecard.index:
        scorecard.at[row, 'FinalScore'] = (
            scorecard.at[row, 'OnTimeDelivery'] * 0.5 +
            (1 - scorecard.at[row, 'DefectRate']) * 0.3 +
            scorecard.at[row, 'SupplierRating'] * 0.2
        )

    # Group by 'SupplierName' and calculate the average score
    scorecard = scorecard.drop(columns=['OnTimeDelivery', 'DefectRate', 'SupplierRating'])
    scorecard = scorecard.groupby('SupplierName').mean().reset_index()
    scorecard = scorecard.sort_values(by='FinalScore', ascending=False)

    return scorecard

if __name__ == "__main__":
    scorecard = create_supplier_scorecard(filepath)
    print("\nSupplier Scorecard:\n", scorecard)
    # Save the scorecard to a new CSV file
    scorecard.to_csv("knowledge/supplier_scorecard.csv", index=False)