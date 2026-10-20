from pathlib import Path
from uuid import uuid4
import aiofiles


WARRANTY_FOLDER = Path("uploads/warranty docs")


class FileHandler:
    async def save_file(self , photo ,folder ,extensions):
        extension = Path(photo.filename).suffix.lower()
        if extension not in extensions:
            raise ValueError("Only JPG and PNG photos are allowed")

        file_name = f"{uuid4().hex}{extension}"
        file_path = Path(folder, file_name) 
        content = await photo.read()
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(content)

        return file_name, str(file_path)