from shellsmith import services


def nuke() -> None:
    print("☣️ Deleting all Shells and Submodels!")
    print("☢️ Deleting all Shells and Submodels!")
    print("⚠️ Deleting all Shells and Submodels!")
    services.delete_all_shells()
    services.delete_all_submodels()
