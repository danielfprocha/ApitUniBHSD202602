from fastapi import APIRouter, HTTPException

from app.repositories import registro as repo
from app.schemas.registro import RegistroBase, RegistroResponse

router = APIRouter(prefix="/registros", tags=["registros"])


@router.post("", response_model=RegistroResponse, status_code=201)
def criar_registro(registro: RegistroBase):
    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="O título não pode estar em branco.")
    try:
        return repo.criar(registro)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@router.get("", response_model=list[RegistroResponse], status_code=200)
def listar_registros():
    return repo.listar()


@router.get("/{registro_id}", response_model=RegistroResponse, status_code=200)
def buscar_registro(registro_id: int):
    registro = repo.buscar_por_id(registro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    return registro


@router.put("/{registro_id}", response_model=RegistroResponse, status_code=200)
def atualizar_registro(registro_id: int, registro: RegistroBase):
    try:
        atualizado = repo.atualizar(registro_id, registro)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    if atualizado is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado para atualização.")
    return atualizado


@router.delete("/{registro_id}", status_code=200)
def deletar_registro(registro_id: int):
    if not repo.deletar(registro_id):
        raise HTTPException(status_code=404, detail="Registro não encontrado para exclusão.")
    return {"mensagem": "Registro removido com sucesso."}