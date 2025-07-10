# Desafio Final - API de Produtos com FastAPI e MongoDB

Este projeto é uma API para gerenciamento de produtos desenvolvida com FastAPI, MongoDB e Pydantic. As últimas atualizações incluem melhorias no tratamento de erros, atualização de dados e filtros avançados.

---

## 📌 Atualizações Implementadas

### 1. Create (Criação de Produto)
- Tratamento de exceções ao inserir produtos no banco.
- Exceção `InsertException` lançada em caso de erro na inserção.
- Erro HTTP 500 retornado para o cliente com mensagem amigável.

### 2. Update (Atualização de Produto)
- Método PATCH modificado para lançar `NotFoundException` caso o produto não seja encontrado.
- Exceção tratada na controller, retornando HTTP 404 com mensagem clara.
- Atualização automática do campo `updated_at` para o horário atual se não enviado.
- Permite modificar manualmente o campo `updated_at` via requisição.

### 3. Filtros (Consulta de Produtos)
- Cadastro de produtos com preços variados.
- Implementação de filtro para consulta por faixa de preço (`price_min` e `price_max`).
- Exemplo de filtro: produtos com preço entre 5.000 e 8.000.
- Endpoint GET `/products` suporta parâmetros de filtro opcionais.

---

## 🚀 Exemplos de Uso

### Criar Produto

```http
POST /products
Content-Type: application/json

{
  "name": "Produto X",
  "quantity": 10,
  "price": 6000.50,
  "status": true
}
