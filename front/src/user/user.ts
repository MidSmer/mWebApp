export class User {
  constructor(
    public id: number,
    public name: string,
    private password?: string
  ) { }
}
