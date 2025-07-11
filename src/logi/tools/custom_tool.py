from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

# Defining a custom tool for the calculation

class CarrierScoringToolInput(BaseModel):
    """Input schema for CarrierScoringTool."""
    csv_path: str = Field(..., description="Path to the CSV file containing carrier data.")

class CarrierScoringTool(BaseTool):
    name: str = "Carrier Scoring Tool"
    description: str = (
        "This tool scores carriers based on historical performance data."
    )
    args_schema: Type[BaseModel] = CarrierScoringToolInput

    def _run(self, csv_path: str) -> pd.DataFrame:
        """
        Create a carrier scorecard from the provided CSV file.
        Args:
            file_path (str): Path to the CSV file containing carrier data.
        Returns:
            pd.DataFrame: A DataFrame containing the carrier scorecard.
        """
        df = pd.read_csv(csv_path)
        required_cols = ['CarrierName', 'OnTime', 'Damaged', 'CustomerRating']
        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if not col in df.columns]
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        scorecard = df[required_cols].copy()
        print(scorecard.head())

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

        return scorecard