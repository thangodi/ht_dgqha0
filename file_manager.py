import os
import shutil
import time
from datetime import datetime

class FileManager:
    """
    FileManager: kezeli a kiterjesztés szerinti áthelyezést.
    sort_by_extension(ext, src_dir, target_root) -> (moved_count, log_path)
    """

    def _safe_username(self):
        try:
            return os.getlogin()
        except Exception:
            return os.environ.get("USERNAME") or os.environ.get("USER") or "Ismeretlen"

    def sort_by_extension(self, ext, src_dir, target_root):
        """
        ext: kiterjesztés (pont nélkül): 'pdf', 'jpg', stb.
        src_dir: forrás mappa (ahonnan a fájlokat olvassuk)
        target_root: a kiválasztott cél szülő mappa; ezen belül jön létre az <ext> almappa
        """
        start_time = time.time()
        pid = os.getpid()
        user = self._safe_username()

        # cél almappa a megadott target_root-on belül
        target_dir = os.path.join(target_root, ext)
        os.makedirs(target_dir, exist_ok=True)

        found_files = []

        # log fájl dátummal/idővel
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"rendezesi_log_{timestamp}.txt"
        log_path = os.path.join(target_dir, log_filename)

        # Végigmegyünk a forrás mappa FŐ fájljain (nem rekurzív)
        for name in os.listdir(src_dir):
            src_path = os.path.join(src_dir, name)
            if os.path.isfile(src_path) and name.lower().endswith("." + ext.lower()):
                dest = os.path.join(target_dir, name)

                # Ha már létezik, sorszámozzuk
                if os.path.exists(dest):
                    base, extension = os.path.splitext(name)
                    i = 1
                    while True:
                        new_name = f"{base}_{i}{extension}"
                        new_dest = os.path.join(target_dir, new_name)
                        if not os.path.exists(new_dest):
                            dest = new_dest
                            break
                        i += 1

                shutil.move(src_path, dest)
                found_files.append(os.path.basename(dest))

        # Naplózás (PID, user, idő, forrás, cél, fájlok, futásidő)
        elapsed = time.time() - start_time
        with open(log_path, "w", encoding="utf-8") as log:
            log.write(f"PID: {pid}\n")
            log.write(f"User: {user}\n")
            log.write(f"Idő (kezdés): {timestamp}\n")
            log.write(f"Forrás mappa: {src_dir}\n")
            log.write(f"Cél mappa: {target_dir}\n")
            log.write("----------------------------------------------------------------\n")

            if found_files:
                log.write("Áthelyezett fájlok:\n")
                for f in found_files:
                    log.write(f"{f}\n")
            else:
                log.write("Nem található egyező fájl.\n")

            log.write("----------------------------------------------------------------\n")
            log.write(f"Futásidő: {int(elapsed // 60)} min {int(elapsed % 60)} sec\n")
            log.write("----------------------------------------------------------------\n")

        return len(found_files), log_path
